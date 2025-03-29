import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Teste {
    id:number;
    nomeTeste:string;
}

@Injectable({
  providedIn: 'root'
})


export class TesteService {
  private url = 'http://127.0.0.1:8000/testes/'

  constructor(private http: HttpClient) {}

  getTestes():Observable<Teste[]>{
    return this.http.get<Teste[]>(this.url);
  }
}
