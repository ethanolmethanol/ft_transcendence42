import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import {HTTP_INTERCEPTORS, HttpClientModule, HttpClientXsrfModule} from "@angular/common/http";
import { AuthService } from './services/auth/auth.service';
import { RouterModule } from '@angular/router';
import { AppComponent } from './app.component';
import { routes } from './app.routes';
import {CsrfInterceptor} from "./session-expired-interceptor";

@NgModule({
  imports: [
    BrowserModule,
    RouterModule.forRoot(routes),
    HttpClientModule,
    HttpClientXsrfModule.withOptions({
      cookieName: 'csrftoken',
      headerName: 'X-CSRFToken',
    }),
  ],
  providers: [
    AuthService,
    { provide: HTTP_INTERCEPTORS, useClass: CsrfInterceptor, multi: true },
  ],
  bootstrap: [AppComponent]
})

export class AppModule { }
