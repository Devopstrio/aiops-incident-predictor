import React, { useEffect } from 'react';
import { useRouter } from 'next/router';

// AIOps Incident Predictor - Landing / Redirect Page
export default function Home() {
    const router = useRouter();

    useEffect(() => {
        // Redirect to the SRE Command Center dashboard by default
        router.push('/dashboard');
    }, [router]);

    return (
        <div className="min-h-screen bg-[#020617] text-white flex items-center justify-center">
            <div className="flex flex-col items-center">
                <div className="w-16 h-16 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin mb-4"></div>
                <h1 className="text-xl font-bold tracking-widest text-slate-400">INITIALIZING COMMAND CENTER...</h1>
            </div>
        </div>
    );
}
