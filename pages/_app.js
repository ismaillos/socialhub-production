
import "@/styles/globals.css";
import Head from "next/head";

export default function App({ Component, pageProps }) {
  return (
    <>
      <Head>
        <title>Viralobby Studio v7</title>
      </Head>
      <Component {...pageProps} />
    </>
  );
}
