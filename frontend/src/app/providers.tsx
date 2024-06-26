"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useState, PropsWithChildren } from "react";

export default function Providers({ children }: PropsWithChildren) {
  const [client] = useState(new QueryClient());

  return <QueryClientProvider client={client}>{children}</QueryClientProvider>;
}
