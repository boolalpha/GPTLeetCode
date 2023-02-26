import '../styles/reset.css'
import '@/styles/globals.css'

import { useEffect } from 'react'
import { useRouter } from 'next/router'
import * as ga from '../lib/ga'



export default function App({ Component, pageProps }) {
    const router = useRouter()

    useEffect(() => {
        const handleRouteChange = (url) => {
        ga.pageview(url)
        }
        //When the component is mounted, subscribe to router changes
        //and log those page views
        router.events.on('routeChangeComplete', handleRouteChange)

        // If the component is unmounted, unsubscribe
        // from the event with the `off` method
        return () => {
        router.events.off('routeChangeComplete', handleRouteChange)
        }
    }, [router.events])


  return <Component {...pageProps} />
}
