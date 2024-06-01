import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { AppComponent } from './app.component';
import { routes } from './app.routes';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import {ConnectionService} from "./services/connection/connection.service";

@NgModule({
  imports: [
    BrowserModule,
    RouterModule.forRoot(routes),
    FormsModule,
    CommonModule,
  ],
  providers: [
    ConnectionService,
  ],
  bootstrap: [AppComponent]
})

export class AppModule { }
