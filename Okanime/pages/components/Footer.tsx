import React from 'react'
import Link from 'next/link';
import {useRouter} from 'next/navigation'


function Footer() {
  return (
    <footer className='border-b border-gray-400 h-100 font-sans font-extrabold bg-custom-blue text-white'>
        <div className="flex flex-col gap-2">
            <div className="flex flex-row gap-10 mr-20 ml-10">
                <div className="flex flex-col gap-5 mt-10">
                    <p>WHO ARE WE?</p>
                    <p>Okanime is your favorite catalogue with the least ads possible that <br></br>is created by animation passionates and APAC diverstissement.</p>
                </div>
                <div className="flex gap-10 h-44 mt-10">
                    <div className="flex flex-col gap-2">
                        <Link href="/catalogue">Legal</Link>
                        <p> Okanime does not host any videos on its server. <br />Contact the video hosting platform directly for any claims <br />of rights relating to the content in question.</p>
                    </div>
                    <div className="flex flex-col gap-2">
                        <Link href="/catalogue">Contact</Link>
                        <p>Discord</p>
                        <p>Twitter</p>
                    </div>
                </div>
            </div>
        </div>
    </footer>
  )
}

export default Footer
