import { cookies } from "next/headers";

export default async function MePage() {
  const token = (await cookies()).get("cdss_access")?.value;

  const res = await fetch("http://localhost:8000/auth/me", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
    cache: "no-store",
  });

  const user = await res.json();

  return (
    <div className="p-6">
      <h1>Current User</h1>
      <pre>{JSON.stringify(user, null, 2)}</pre>
    </div>
  );
}
