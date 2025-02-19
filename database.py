import psycopg2
from psycopg2.extras import RealDictCursor
from config import DATABASE_URL

def get_connection():
    try:
        return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        return None

def is_ip_blocked(ip):
    """Checks if the IP address is blocked."""
    conn = get_connection()
    if not conn:
        return False
    
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM blocked_ips WHERE ip_address = %s", (ip,))
            blocked = cur.fetchone() is not None
    conn.close()
    return blocked

def add_rate_limit(key, request_limit):
    conn = get_connection()
    if not conn:
        return
    
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO rate_limits (key, request_limit, remaining, reset_at)
                VALUES (%s, %s, %s, NOW() + INTERVAL '1 hour')
                ON CONFLICT (key) DO UPDATE SET remaining = %s, reset_at = NOW() + INTERVAL '1 hour'
                """,
                (key, request_limit, request_limit, request_limit)
            )
    conn.close()

def update_remaining(key, remaining):
    """Updates the remaining number of requests."""
    conn = get_connection()
    if not conn:
        return
    
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE rate_limits SET remaining = %s WHERE key = %s",
                (remaining, key)
            )
    conn.close()

def block_ip(ip, reason="Suspicious activity"):
    """Adds IP to the blocked list."""
    conn = get_connection()
    if not conn:
        return
    
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO blocked_ips (ip_address, reason) VALUES (%s, %s) ON CONFLICT (ip_address) DO NOTHING",
                (ip, reason)
            )
    conn.close()
