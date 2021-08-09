import Head from "next/head";
import { useEffect, useState } from "react";
import useSWR from "swr";
import styles from "./index.module.css";

const fetcher = async (url: string) => {
  const res = await fetch(url);

  // If the status code is not in the range 200-299,
  // we still try to parse and throw it.
  if (!res.ok) {
    const error = new Error("An error occurred while fetching the data.");
    // Attach extra info to the error object.
    (error as any).info = await res.json();
    (error as any).status = res.status;
    throw error;
  }

  return res.json();
};

const example = "dogs playing in the snow";

const gifs = [
  "https://media.giphy.com/media/UxREcFThpSEqk/giphy.gif",
  "https://media.giphy.com/media/xf20D8HzvTQzu/giphy.gif",
  "https://media.giphy.com/media/hCiQVo1dzVwPu/giphy.gif",
  "https://media.giphy.com/media/oT7ATDykMidsk/giphy.gif",
  "https://media.giphy.com/media/3o7TKxOhkp8gO0LXMI/giphy.gif",
  "https://media.giphy.com/media/lSZCmfg8STSBa/giphy.gif",
  "https://media.giphy.com/media/3kACvwjyzgOdqE3GWT/giphy.gif",
  "https://media.giphy.com/media/5wWf7H0qoWaNnkZBucU/giphy.gif",
];

function getLoadingGif() {
  return gifs[Math.floor(Math.random() * gifs.length)];
}

export default function Home() {
  const db = "opensearch";
  const [searchBarValue, setSearchBarValue] = useState("");
  const [gif, setGif] = useState(getLoadingGif());
  const query = useDebounce(searchBarValue, 1000);
  const { data: response, error, isValidating } = useSWR(
    () =>
      query &&
      searchBarValue === query &&
      `${process.env.NEXT_PUBLIC_API_URL}?search=${encodeURIComponent(query)}&db=${db}`,
    fetcher,
    { revalidateOnFocus: false }
  );
  const searching = isValidating;

  return (
    <div className="relative">
      <Head>
        <title>Helios</title>
        <meta
          name="description"
          content="Image search engine. Powered by machine learning."
        />
        <link rel="icon" href="/sun.png" />
      </Head>
      <a href="https://github.com/rkouye/es-clip-image-search">
        <img
          src="/github-logo.svg"
          alt="github"
          className="h-6 fixed z-20 top-4 right-4"
        />
      </a>
      <header className="w-full sticky top-0 z-10 bg-light shadow py-4">
        <div className="text-8xl text-center">
          heli
          <img src="/sun.png" alt="github" className="h-12 inline" />s
        </div>
        <p className="text-center text-xs text-gray-500 mt-5">
          Search image by description
        </p>
        <div className="mx-auto max-w-xl p-4 relative">
          <svg
            height="24px"
            viewBox="0 0 24 24"
            width="24px"
            fill="currentColor"
            className={`text-primary absolute right-8 top-7 ${
              searching ? "animate-spin" : ""
            }`}>
            <path d="M0 0h24v24H0V0z" fill="none" />
            <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z" />
          </svg>
          <input
            className={`${styles.searchBar} text-gray-600`}
            type="text"
            onChange={(e) => setSearchBarValue(e.target.value)}
            value={searchBarValue}
            placeholder={`Type something here, example : ${example}`}
            autoFocus
          />
        </div>
      </header>
      {searching && (
        <div className="mx-auto max-w-6xl">
          <img src={gif} className="mx-auto my-2" />
          <p className="text-center">
            Search can take around 30 seconds
            <button
              onClick={() => setGif(getLoadingGif())}
              className="text-primary px-2">
              change gif
            </button>
          </p>
        </div>
      )}
      <main
        className={`m-4 ${
          searching ? "opacity-0" : "opacity-100"
        } transition-all`}>
        {error && (
          <code className="text-danger p-2 text-center">
            Looks like the search service is down. Wait a little, and try again.
          </code>
        )}
        {!error && response && response.hits && (
          <ul className="mx-auto max-w-6xl grid grid-cols-1 gap-4 lg:grid-cols-3">
            {response.hits.hits.map((hit: any, index: number) => (
              <li
                key={index}
                className="text-gray-900 p-4 bg-gray-50 shadow rounded-lg flex flex-col justify-center"
                style={{ minHeight: "200px" }}>
                <img
                  src={hit.url}
                  className="w-full"
                />
                <a
                  href={hit.url}
                  className="text-primary underline">
                  source
                </a>
              </li>
            ))}
          </ul>
        )}

        {response && (
          <footer className="mt-16 text-center">
            Made by{" "}
            <a href="https://github.com/rkouye" className="text-primary">
              <b>rkouye</b>
            </a>
            . Please, note that I do not own any of these pictures. Every
            picture is linked back to its original source. This is <b>NOT</b> an
            image distribution service.
          </footer>
        )}
      </main>
    </div>
  );
}

function useDebounce<T>(value: T, delay: number) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}
