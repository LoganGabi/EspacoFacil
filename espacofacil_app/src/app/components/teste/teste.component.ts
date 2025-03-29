import { Component, OnInit } from '@angular/core';
import { Teste, TesteService } from 'src/app/services/teste.service';

@Component({
  selector: 'app-teste',
  templateUrl: './teste.component.html',
  styleUrls: ['./teste.component.scss']
})
export class TesteComponent implements OnInit {
  testes:Teste[] = [];

  constructor(private testeService:TesteService){}
  ngOnInit(): void {
    this.loadTestes();
  }

  loadTestes(){
    this.testeService.getTestes().subscribe(data => {
      this.testes = data;
    })
  }
}
