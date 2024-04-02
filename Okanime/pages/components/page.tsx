import Image from "next/image";
import Link from 'next/link';
import Anime from "../catalogue/[animeName]/index";
import Header from "./Header";
import "./layout.css"

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <Header />
      {/* <Anime /> */}
      <Link
        href="/catalogue/[animeName]/[season]/[language]"
        as={`/catalogue/solo-leveling/saison1/vostfr`}
      >
        <p>Watch Solo Leveling</p>
      </Link>
    </main>
  );
}
