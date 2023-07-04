import { IProperty } from "../pages/adminPage/components/interfaces";
import { Cookies } from 'react-cookie';
const cookies = new Cookies();
const credentials = 'credentials';

const getCookie = async () => cookies.get(credentials);

const BASE_URL = import.meta.env.VITE_BASE_URL

interface IResponse {
  success: boolean;
  error: any | null;
  message: string | null
  result: any;
  status?: number;

}

export const submitCredentials = async (data: { email: string, password: string, username: string }) => {

  try {
    const url = `${BASE_URL}/users`;
    const request = await fetch(url, {
      method: "POST",
      body: JSON.stringify(data),
      headers: new Headers({
        'Content-Type': 'application/json',
        'authorization': 'cookieValue.token'
      }),
    });

    return request;

  } catch (error) {
    return null
  }
}

export const login = async (data: { email: string, password: string, username: string }): Promise<null | IResponse> => {
  try {
    const url = `${BASE_URL}/login`;
    const request = await fetch(url, {
      method: "POST",
      body: JSON.stringify(data),
      headers: new Headers({
        'Content-Type': 'application/json'
      }),
    });
    const response = await request.json()
    return {
      ...response,
      status: request?.status
    }
  } catch (error) {
    return null
  }
}

export const createProperty = async (
  data: Omit<IProperty, 'images'>
): Promise<null | IResponse> => {
  const {token} = await getCookie();
  try {
    const url = `${BASE_URL}/properties`;
    const request = await fetch(url, {
      method: "POST",
      body: JSON.stringify(data),
      headers: new Headers({
        'Content-Type': 'application/json',
        'Authorization': token,
      }),
    });
    const response = await request.json()
    return {
      ...response,
      status: request?.status
    }
  } catch (error) {
    return null
  }
}

export const createPropertyImages = async (
  data: {list_str_binary: string[], property_id: number }
): Promise<null | IResponse> => {
  const {token} = await getCookie();
  try {
    const url = `${BASE_URL}/images/batch`;
    const request = await fetch(url, {
      method: "POST",
      body: JSON.stringify(data),
      headers: new Headers({
        'Content-Type': 'application/json',
        'Authorization': token,
      }),
    });
    const response = await request.json()
    return {
      ...response,
      status: request?.status
    }
  } catch (error) {
    return null
  }
}