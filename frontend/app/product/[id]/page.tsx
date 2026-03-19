"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

export default function ProductPage() {
  const params = useParams();
  const id = params.id as string;

  const [data, setData] = useState<any>(null);

  useEffect(() => {
    if (!id) return;

    fetch(`http://127.0.0.1:8000/products/${id}`)
      .then((res) => res.json())
      .then((json) => setData(json));
  }, [id]);

  if (!data) {
    return <div className="min-h-screen bg-black text-white p-10">Yükleniyor...</div>;
  }

  return (
    <div className="min-h-screen bg-black text-white p-10">
      <h1 className="text-3xl font-bold mb-4">{data.name}</h1>
      <p className="text-green-400 font-bold mb-6">En ucuz: {data.best_price} TL</p>

      <div className="space-y-3">
        {data.offers.map((offer: any, index: number) => (
          <div
            key={index}
            className="bg-gray-900 p-4 rounded flex justify-between items-center"
          >
            <div>
              <p className="font-semibold">{offer.store}</p>
              <p className="text-green-400">{offer.price} TL</p>
            </div>

            <a
              href={offer.url}
              target="_blank"
              rel="noopener noreferrer"
              className="bg-blue-500 px-3 py-2 rounded text-sm"
            >
              Satın al
            </a>
          </div>
        ))}
      </div>
    </div>
  );
}