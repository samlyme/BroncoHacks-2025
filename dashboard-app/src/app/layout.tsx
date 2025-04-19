import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { AppRouterCacheProvider } from '@mui/material-nextjs/v15-appRouter';
 // or `v1X-appRouter` if you are using Next.js v1X

 export default function RootLayout(props: { children: React.ReactNode }) {
   return (
     <html lang="en">
       <body>
+        <AppRouterCacheProvider>
           {props.children}
+        </AppRouterCacheProvider>
       </body>
     </html>
   );
 }

