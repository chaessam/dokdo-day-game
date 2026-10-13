// 독도 원정대 Cloudflare Worker: 정적 파일을 내보내고, 참여 기기 수·플레이 수만 센다 (로그인·개인정보 없음)
import { DurableObject } from "cloudflare:workers";

const ID_RE = /^[a-z0-9]{16,40}$/;
const NEW_DEVICES_PER_IP_PER_DAY = 600;   // 학교는 여러 기기가 같은 IP를 쓰므로 넉넉하게
const REPLAY_GAP_MS = 10 * 60 * 1000;     // 같은 기기는 10분에 한 번만 플레이로 센다
const STATS_CACHE_MS = 30 * 1000;

export class Stats extends DurableObject {
  constructor(ctx, env) {
    super(ctx, env);
    this.sql = ctx.storage.sql;
    this.sql.exec(`
      CREATE TABLE IF NOT EXISTS devices (id TEXT PRIMARY KEY, plays INTEGER NOT NULL DEFAULT 0, first INTEGER, last INTEGER);
      CREATE TABLE IF NOT EXISTS counters (name TEXT PRIMARY KEY, value INTEGER NOT NULL DEFAULT 0);
      CREATE TABLE IF NOT EXISTS ip_limits (ip TEXT NOT NULL, day INTEGER NOT NULL, count INTEGER NOT NULL DEFAULT 0, PRIMARY KEY (ip, day));
    `);
    this.cache = null;
  }
  counter(name) {
    const row = this.sql.exec("SELECT value FROM counters WHERE name = ?", name).toArray()[0];
    return row ? row.value : 0;
  }
  bump(name) {
    this.sql.exec("INSERT INTO counters (name, value) VALUES (?, 1) ON CONFLICT (name) DO UPDATE SET value = value + 1", name);
  }
  stats() {
    if (this.cache && Date.now() - this.cache.at < STATS_CACHE_MS) return this.cache.data;
    const data = { players: this.counter("players"), plays: this.counter("plays") };
    this.cache = { at: Date.now(), data };
    return data;
  }
  play(id, ip) {
    const now = Date.now(), day = Math.floor(now / 864e5);
    const row = this.sql.exec("SELECT last FROM devices WHERE id = ?", id).toArray()[0];
    if (!row) {
      const lim = this.sql.exec("SELECT count FROM ip_limits WHERE ip = ? AND day = ?", ip, day).toArray()[0];
      if (lim && lim.count >= NEW_DEVICES_PER_IP_PER_DAY) return this.stats();
      this.sql.exec("INSERT INTO ip_limits (ip, day, count) VALUES (?, ?, 1) ON CONFLICT (ip, day) DO UPDATE SET count = count + 1", ip, day);
      this.sql.exec("DELETE FROM ip_limits WHERE day < ?", day - 2);
      this.sql.exec("INSERT INTO devices (id, plays, first, last) VALUES (?, 1, ?, ?)", id, now, now);
      this.bump("players"); this.bump("plays");
    } else if (now - row.last > REPLAY_GAP_MS) {
      this.sql.exec("UPDATE devices SET plays = plays + 1, last = ? WHERE id = ?", now, id);
      this.bump("plays");
    } else return this.stats();
    this.cache = null;
    return this.stats();
  }
}

const json = (data, status = 200) => new Response(JSON.stringify(data), { status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" } });
const statsOf = (env) => env.STATS.get(env.STATS.idFromName("main"));

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (url.pathname.startsWith("/api/")) {
      // 통계가 고장 나도 게임은 그대로 돌아가도록, 오류는 JSON으로만 알린다
      try {
        if (!env.STATS) return json({ error: "STATS binding missing" }, 503);
        if (url.pathname === "/api/stats" && req.method === "GET") return json(await statsOf(env).stats());
        if (url.pathname === "/api/play" && req.method === "POST") {
          const body = await req.json().catch(() => ({}));
          const id = String((body && body.id) || "");
          if (!ID_RE.test(id)) return json({ error: "bad id" }, 400);
          return json(await statsOf(env).play(id, req.headers.get("cf-connecting-ip") || "unknown"));
        }
        return json({ error: "not found" }, 404);
      } catch (e) {
        return json({ error: String((e && e.stack) || e) }, 500);
      }
    }
    return env.ASSETS.fetch(req);
  },
};
