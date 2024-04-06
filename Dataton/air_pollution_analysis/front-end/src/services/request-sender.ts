import { Input } from "@/data-models/input";
import axios from "axios";

export class RequestSender{

    private url : string

    headers = {
        'Content-Type': 'application/json',
      }

    constructor(){
        console.error(process.env)
        if(process.env['NEXT_PUBLIC_REQUEST_URL'] == undefined){
            this.url ="http://127.0.0.1:5000/predict"
        }
        else{
            this.url = process.env['NEXT_PUBLIC_REQUEST_URL']
        }
  
    }
    
    async sendRequest(method: string,  data: Input[]): Promise<number[]> {
        console.warn(data)
        let res = await axios.post(this.url, 
            {
            model: method,
            series: data
        }, {
            headers: this.headers
        })
        console.log(res.data)
        return res.data;
    }
}