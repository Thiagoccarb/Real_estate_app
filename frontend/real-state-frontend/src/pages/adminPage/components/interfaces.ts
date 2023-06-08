import { brazilianStates } from "./states";

export interface IProperty {
  name: string;
  action: 'rent' | 'sale';
  type: 'house' | 'apartament';
  description: string;
  bedrooms: number;
  bathrooms: number;
  price: number;
  address: {
    street_name:string;
		number: number | string;
		cep: string;
  };
  images: string[];
  city: {
    state: typeof brazilianStates[number]['abbreviation'] | '',
    name: string;
  },
}