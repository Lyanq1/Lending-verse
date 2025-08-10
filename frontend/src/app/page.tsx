import { TransactionCircle } from "@/components/ui/transaction-circle";

const partners = [
  {
    id: "1",
    name: "Shopee",
    logo: "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Shopee_logo.svg/1442px-Shopee_logo.svg.png",
    type: "business" as const,
  },
  {
    id: "2",
    name: "Tiki",
    logo: "https://storage.googleapis.com/hust-files/images/tiki_21.1k.png",
    type: "business" as const,
  },
  {
    id: "3",
    name: "FPT",
    logo: "https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/FPT_logo_2010.svg/2560px-FPT_logo_2010.svg.png",
    type: "business" as const,
  },
  {
    id: "4",
    name: "VNG",
    logo: "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/VNG_Corp._logo.svg/1200px-VNG_Corp._logo.svg.png",
    type: "business" as const,
  },
  {
    id: "5",
    name: "Individual Lender",
    logo: "https://images.rawpixel.com/image_png_800/cHJpdmF0ZS9sci9pbWFnZXMvd2Vic2l0ZS8yMDIzLTAxL3JtNjA5LXNvbGlkaWNvbi13LTAwMi1wLnBuZw.png",
    type: "individual" as const,
  },
  {
    id: "6",
    name: "Business Owner",
    logo: "https://cdn-icons-png.flaticon.com/512/9166/9166850.png",
    type: "individual" as const,
  },
];

export default function Home() {
  return (
    <main className="flex min-h-screen pt-32 px-24 pb-24">
      <div className="flex flex-row w-full gap-12">
        {/* Left column - Text content */}
        <div className="flex-1 flex flex-col justify-center">
          <h1 className="text-5xl font-bold mb-8">
            Revolutionizing P2P Lending
          </h1>
          <div className="space-y-6 text-lg">
            <p>
              LendingVerse connects businesses and individuals through a secure and efficient P2P lending platform.
            </p>
            <p>
              Our innovative approach eliminates traditional banking barriers, enabling direct lending relationships between investors and borrowers.
            </p>
            <p>
              Whether you&apos;re a business seeking growth capital or an individual looking to invest, our platform provides a transparent and reliable lending ecosystem.
            </p>
            <button className="mt-8 px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
              Get Started
            </button>
          </div>
        </div>

        {/* Right column - Animation */}
        <div className="flex-1 flex items-center justify-center">
          <TransactionCircle partners={partners} />
        </div>
      </div>
    </main>
  );
}