import Image from "next/image";
import Anime from "../component/Anime";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <h1>Welcome to OkAnime</h1>
      <Anime />
    </main>
  );
}
