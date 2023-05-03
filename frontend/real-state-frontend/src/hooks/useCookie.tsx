import { useCookies } from 'react-cookie';

interface CookieSetOptions {
  path?: string;
  expires?: Date;
  maxAge?: number;
  domain?: string;
  secure?: boolean;
  httpOnly?: boolean;
  sameSite?: boolean | 'none' | 'lax' | 'strict';
  encode?: (value: string) => string;
}

export function useCookie(key: string) {
  const [cookies, setCookie] = useCookies([key]);

  const updateCookie = (value: string, options: CookieSetOptions | undefined) => {
    setCookie(key, value, options);
  };

  return [cookies[key], updateCookie];
}
