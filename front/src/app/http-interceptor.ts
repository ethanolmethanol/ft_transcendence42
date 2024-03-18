import { Injectable } from '@angular/core';
import { HttpClientModule, HttpClientXsrfModule, HttpInterceptor, HttpXsrfTokenExtractor, HttpRequest, HttpHandler, HttpEvent } from '@angular/common/http'
import { Observable } from 'rxjs';

@Injectable()
export class HttpXSRFInterceptor implements HttpInterceptor {

  constructor(private tokenExtractor: HttpXsrfTokenExtractor){
    console.log("Interceptor created");
  }
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    console.log("Intercepted request: ", req);
    const headerName = 'X-CSRFToken';
    let token = this.tokenExtractor.getToken() as string;
    if (token !== null && !req.headers.has(headerName)){
      req=req.clone({ headers: req.headers.set(headerName, token)})
      console.log("Modified request: ", req);
    }
    return next.handle(req);
  }
}
