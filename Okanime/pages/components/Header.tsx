// components/Header.js

import Image from 'next/image';
import Link from 'next/link';

import styles from '../../styles/Header.module.css';

const Header = () => {
  return (
    <header className={styles.header}>
      <div className={styles.logo}>
        <Image className="header-logo" src="/logo.png" alt="Anime Sama" width={100} height={50} />
      </div>
      <nav className={styles.nav}>
        <Link href="/catalogue">Catalogue</Link>
        <Link href="/planning">Planning</Link>
        <Link href="/help">Aide</Link>
        <Link href="/profil">Profil</Link>
      </nav>
    </header>
  );
};

export default Header;
