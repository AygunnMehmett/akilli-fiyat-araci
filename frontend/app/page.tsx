"use client";

import { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const search = async () => {
    if (!query) return;

    setLoading(true);

    try {
      const res = await fetch(`https://akilli-fiyat-araci-t9eq.vercel.app/search?q=${query}`);
      const data = await res.json();

      const grouped = Object.values(
        (data.results || []).reduce((acc: any, item: any) => {
          if (!acc[item.id]) {
            acc[item.id] = {
              id: item.id,
              product: item.product,
              best_price: item.price,
              offer_count: 1,
            };
          } else {
            acc[item.id].offer_count += 1;
            if (item.price < acc[item.id].best_price) {
              acc[item.id].best_price = item.price;
            }
          }
          return acc;
        }, {})
      );

      setResults(grouped as any[]);
    } catch (error) {
      console.error("Hata:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center p-10">
      
      {/* LOGO */}
      <img src="/logo.png" className="w-12 mb-2" />

      <h1 className="text-3xl font-bold mb-6">
        💸 Akıllı Fiyat Karşılaştırma
      </h1>

      <div className="flex gap-2 mb-6">
        <input
          className="p-3 text-black rounded min-w-[260px]"
          placeholder="Ürün ara (örn: logitech)"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button onClick={search} className="bg-blue-500 px-4 rounded">
          Ara
        </button>
      </div>

      {loading && <p>Yükleniyor...</p>}

      <div className="w-full max-w-xl">
        {results.map((item: any) => (
          <div
            key={item.id}
            onClick={() => (window.location.href = `/product/${item.id}`)}
            className="bg-gray-900 p-4 mb-3 rounded flex justify-between cursor-pointer hover:bg-gray-800"
          >
            <div>
              <p className="font-bold">{item.product}</p>
              <p className="text-sm text-gray-400">
                {item.offer_count} mağazada var
              </p>
            </div>

            <div className="text-right">
              <p className="text-green-400 font-bold">
                {item.best_price} TL
              </p>
              <p className="text-xs text-gray-400">
                En ucuz fiyat
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}