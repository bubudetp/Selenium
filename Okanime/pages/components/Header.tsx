// components/Header.js
import {useState} from 'react';
import Image from 'next/image';
import Link from 'next/link';
import {useRouter} from 'next/navigation'
import "../globals.css";

const Header = () => {

  const router = useRouter();
  const [inputValue, setInputValue] = useState('');

  const handleInputSubmit = (e) => {
    if (e.key === 'Enter'){
      router.push(`/catalogue/${inputValue}`)
    }
  }
  const handleInputChange = (e) => {
    setInputValue(e.target.value)
  }

  return (
    <header className=" border-b border-gray-400 h-100 font-sans font-extrabold bg-custom-blue text-white">
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
          <input
              type="text"
              value={inputValue}
              onChange={handleInputChange}
              onKeyDown={handleInputSubmit}
              className="text-black font-normal"
            />
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