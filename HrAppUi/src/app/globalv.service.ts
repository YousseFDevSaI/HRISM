import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class GlobalvService {

  private UserEmail :string = "None";
  constructor() { }

  setEmail(email: string){
    this.UserEmail = email
  }
  getEmail(){
    return this.UserEmail
  }
}
