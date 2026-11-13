import React from 'react';
import { Header } from "@/components/ui/header-2";
import { MagnificationDock } from "@/components/ui/magnification-dock";
import { Home, Search, Settings, User, Bell, Mail, Camera, Heart } from 'lucide-react';

export default function Demo() {
  const items = [
    { icon: <Home size={22} />, label: 'Home', onClick: () => console.log('Home') },
    { icon: <Search size={22} />, label: 'Search', onClick: () => console.log('Search') },
    { icon: <User size={22} />, label: 'Profile', onClick: () => console.log('Profile') },
    { icon: <Bell size={22} />, label: 'Notifications', onClick: () => console.log('Notifications') },
    { icon: <Mail size={22} />, label: 'Messages', onClick: () => console.log('Messages') },
    { icon: <Camera size={22} />, label: 'Capture', onClick: () => console.log('Capture') },
    { icon: <Heart size={22} />, label: 'Likes', onClick: () => console.log('Likes') },
    { icon: <Settings size={22} />, label: 'Settings', onClick: () => console.log('Settings') },
  ];

  return (
    <div className="w-full">
      <Header />

      <main className="mx-auto min-h-screen w-full max-w-3xl px-4 py-12 flex flex-col items-center">
        <h1 className="text-2xl font-bold mb-8">Magnification Dock Demo</h1>
        
        <div className="my-8 w-full flex justify-center">
          <MagnificationDock 
            items={items}
            panelHeight={68}
            baseItemSize={50}
            magnification={80}
          />
        </div>

        <div className="space-y-2 mb-4 w-full">
          <div className="bg-accent h-6 w-4/6 rounded-md border" />
          <div className="bg-accent h-6 w-1/2 rounded-md border" />
        </div>
      </main>
    </div>
  );
}
