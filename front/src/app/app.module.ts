import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import {HTTP_INTERCEPTORS, HttpClientModule} from "@angular/common/http";
import { AuthService } from './services/auth.service';
import { RouterModule } from '@angular/router';
import { AppComponent } from './app.component';
import { routes } from './app.routes';

@NgModule({
  imports: [
    BrowserModule,
    RouterModule.forRoot(routes),
    HttpClientModule
  ],
  providers: [
    AuthService,
    // { provide: HTTP_INTERCEPTORS, useClass: CrsfInterceptor, multi: true },
  ],
  bootstrap: [AppComponent]
})

export class AppModule { }
