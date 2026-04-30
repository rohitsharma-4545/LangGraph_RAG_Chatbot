export async function getToken(role: "user" | "admin", password?: string) {
  const res = await fetch(`${process.env.BACKEND_URL}/token`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user_id: "test",
      role,
      password: role === "admin" ? password : null,
    }),
  });

  return res.json();
}
