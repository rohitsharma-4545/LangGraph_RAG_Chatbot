"use client";

import { useState } from "react";

export function useAdmin() {
  const [isAdmin, setIsAdmin] = useState(false);
  const [token, setToken] = useState("");

  const login = async (password: string, role: "admin" | "user") => {
    console.log(password);
    console.log(role);
    try {
      const res = await fetch("/api/auth", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          role,
          password: role === "admin" ? password : null,
        }),
      });

      if (!res.ok) return false;

      const data = await res.json();

      if (data.token) {
        setToken(data.token);
        setIsAdmin(role === "admin");
        return true;
      }

      return false;
    } catch {
      return false;
    }
  };

  const logout = () => {
    setIsAdmin(false);
    setToken("");
  };

  return { isAdmin, token, login, logout };
}
