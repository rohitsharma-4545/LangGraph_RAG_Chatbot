"use client";

import { useState } from "react";

export default function AdminPanel({ token }: { token: string }) {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [showConfirm, setShowConfirm] = useState(false);

  const upload = async (file: File) => {
    setLoading(true);
    setMessage("");

    try {
      const form = new FormData();
      form.append("file", file);

      const res = await fetch("/api/admin/upload", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`, // ✅ unchanged
        },
        body: form,
      });

      if (!res.ok) throw new Error(await res.text());

      setMessage("Upload started successfully");
    } catch (err: any) {
      setMessage(err.message || "Upload failed");
    } finally {
      setLoading(false);
    }
  };

  const deletePdf = async () => {
    setLoading(true);
    setMessage("");

    try {
      const res = await fetch("/api/admin/delete", {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!res.ok) throw new Error(await res.text());

      setMessage("Documents deleted");
    } catch (err: any) {
      setMessage(err.message || "Delete failed");
    } finally {
      setLoading(false);
      setShowConfirm(false); // ✅ close modal
    }
  };

  return (
    <aside className="w-64 border-r bg-white flex flex-col p-5">
      {/* Header */}
      <div className="mb-6">
        <h2 className="text-base font-semibold text-gray-800">Admin Panel</h2>
        <p className="text-xs text-gray-500">Manage documents</p>
      </div>

      {/* Upload Card */}
      <div className="border rounded-xl p-4 mb-4 shadow-sm">
        <p className="text-sm font-medium text-gray-700 mb-3">Upload PDF</p>

        <label className="flex flex-col items-center justify-center border-2 border-dashed border-gray-300 rounded-lg p-4 cursor-pointer hover:border-blue-500 transition">
          <span className="text-sm text-gray-600">
            {loading ? "Uploading..." : "Click to upload"}
          </span>

          <input
            type="file"
            className="hidden"
            disabled={loading}
            onChange={(e) => {
              const file = e.target.files?.[0];
              if (file) upload(file);
            }}
          />
        </label>
      </div>

      {/* Delete Card */}
      <div className="border rounded-xl p-4 shadow-sm">
        <p className="text-sm font-medium text-gray-700 mb-3">Danger Zone</p>

        <button
          onClick={() => setShowConfirm(true)}
          disabled={loading}
          className="w-full text-sm bg-red-50 text-red-600 py-2 rounded-lg hover:bg-red-100 transition disabled:opacity-50"
        >
          Delete All PDFs
        </button>
      </div>

      {/* Status */}
      {message && (
        <div className="mt-4 text-xs text-gray-600 bg-gray-100 p-3 rounded-lg border">
          {message}
        </div>
      )}

      {showConfirm && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl shadow-lg w-80 p-5 space-y-4">
            <h3 className="text-base font-semibold text-gray-800">
              Delete Documents
            </h3>

            <p className="text-sm text-gray-600">
              Are you sure you want to delete all PDFs? This action cannot be
              undone.
            </p>

            <div className="flex justify-end gap-2">
              <button
                onClick={() => setShowConfirm(false)}
                className="text-sm text-gray-500 px-3 py-1"
              >
                Cancel
              </button>

              <button
                onClick={deletePdf}
                disabled={loading}
                className="bg-red-600 text-white px-4 py-1.5 rounded-lg text-sm hover:bg-red-700 disabled:opacity-50"
              >
                {loading ? "Deleting..." : "Delete"}
              </button>
            </div>
          </div>
        </div>
      )}
    </aside>
  );
}
