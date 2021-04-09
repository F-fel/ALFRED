import { Component, Input, OnInit } from '@angular/core';
import {MatFormFieldModule} from '@angular/material/form-field';
import { Drone } from '@app/class/drone';
import { HomePageComponent } from '../page/home/home-page.component';

@Component({
  selector: 'app-init-real-pos',
  templateUrl: './init-real-pos.component.html',
  styleUrls: ['./init-real-pos.component.scss']
})
export class InitRealPosComponent implements OnInit {
  drones: Drone[]= [];
  @Input() numberOfDrones: number;

  constructor(public homepageComponent: HomePageComponent) { }

  ngOnInit(): void {  
  }

  ngOnChanges(): void {
    this.clearDronesList();
    this.createListDrone(this.numberOfDrones);
  }

  public addDrone(id: number): void {
    this.drones.push(new Drone(id));
  }

  public createListDrone(numberOfDrones: number): void {
    for(let i = 0; i < numberOfDrones;  i++){
      this.addDrone(i);
    }
  }

  public clearDronesList(): void {
    this.drones = [];
  }

}


