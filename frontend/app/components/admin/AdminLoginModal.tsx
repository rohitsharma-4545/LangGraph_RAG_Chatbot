"use client";

import { useState } from "react";

export default function AdminLoginModal({
  onClose,
  onLogin,
}: {
  onClose: () => void;
  onLogin: (password: string, role: "admin" | "user") => Promise<boolean>;
}) {
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center">
      <div className="bg-white p-6 rounded-xl w-80 space-y-4">
        <h2 className="font-semibold">Admin Login</h2>

        <input
          type="password"
          className="w-full border p-2 rounded"
          placeholder="Enter password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        {error && <p className="text-red-500 text-sm">{error}</p>}

        <div className="flex justify-end gap-2">
          <button onClick={onClose}>Cancel</button>
          <button
            className="bg-blue-600 text-white px-4 py-1 rounded disabled:opacity-50"
            disabled={!password}
            onClick={async () => {
              setError("");

              const ok = await onLogin(password, "admin");

              if (!ok) {
                setError("Invalid password");
                return;
              }

              setPassword("");
              onClose();
            }}
          >
            Login
          </button>
        </div>
      </div>
    </div>
  );
}
