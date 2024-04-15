// components/Header.js
import Image from 'next/image';
import Link from 'next/link';
import "../globals.css";

const Header = () => {
  return (
    <header className=" border-b border-gray-400 h-100 font-sans font-extrabold bg-custom-brown text-white">
      <div className="flex justify-between ml-4 mr-20">
        <div className="flex items-center">
            <Image
              src="/logo-okami.png"
              alt="logo"
              width={100}
              height={100}
            />
          <h1 className="text-2xl absolute ml-20 mb-1">OKANIME</h1>

        </div>
        <div className="flex row items-center gap-x-8">
          <Link href="/catalogue">CATALOGUE</Link>
          <Link href="/planning">PLANNING</Link>
          <Link href="/help">AIDE</Link>
          <Link href="/profil">PROFIL</Link>
        </div>
      </div>
    </header>
  );
};

export default Header;