import Image from 'next/image';
import Link from 'next/Link';

import styles from '../styles/Menu.module.css'


export default function DesktopMenu(props) {

    const {pages} = props;

    return (
        <div className={styles.desktopMenuContainer}>
            <Link className={styles.logo} href="./">
                <Image src="/GPTLeetCode-Logo.png" alt="Logo" className={styles.logo_image} height={25} width={25}/>
                ChatGPT Leetcode
            </Link>
            <ul className={styles.desktopLinksContainer}>
                {
                    pages.map((page) => {
                        return (
                            <li className={`${styles.desktopListItem} ${page.active ? styles.desktopActivePage : ""}`} key={page.title}>
                                <a className={styles.desktopLink} href={page.link}>{page.title}</a>
                            </li>
                        );
                    }) 
                }
            </ul>
        </div>
    );
}
