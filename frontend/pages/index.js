import Head from 'next/head';
import { useEffect, useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [intel, setIntel] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchIntel() {
      try {
        const res = await axios.get('/api/intel');
        setIntel(res.data.intel);
      } catch (err) {
        console.error(err);
        setError('Failed to load intelligence feed');
      } finally {
        setLoading(false);
      }
    }
    fetchIntel();
  }, []);

  return (
    <>
      <Head>
        <title>EBC Intel Radar</title>
      </Head>
      <main className="max-w-4xl mx-auto p-8">
        <h1 className="text-4xl font-bold mb-6">EBC Intel Radar</h1>
        {loading && <p>Loading…</p>}
        {error && <p className="text-red-600">{error}</p>}
        <ul className="space-y-4">
          {intel.map((item) => (
            <li key={item.id} className="border-b border-gray-200 pb-4">
              <a href={item.url} target="_blank" rel="noopener noreferrer" className="text-xl font-semibold hover:underline">
                {item.title}
              </a>
              <p className="text-gray-500 text-sm">{new Date(item.published).toLocaleString()}</p>
              {item.summary && <p className="mt-2 text-gray-700">{item.summary}</p>}
            </li>
          ))}
        </ul>
        {!loading && intel.length === 0 && (
          <p className="text-gray-600">No intelligence items available yet.</p>
        )}
      </main>
    </>
  );
}
