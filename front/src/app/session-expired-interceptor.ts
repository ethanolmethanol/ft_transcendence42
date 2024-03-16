import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable()
export class CsrfInterceptor implements HttpInterceptor {

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const csrfToken = this.getCookie('csrftoken');
    if (csrfToken) {
      const clonedRequest = req.clone({
        withCredentials: true,
        headers: req.headers.set('X-CSRFToken', csrfToken)
      });
      return next.handle(clonedRequest);
    }
    return next.handle(req);
  }

  private getCookie(name: string): string | null {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
      return parts.pop()?.split(';').shift() || null;
    }
    return null;
  }
}
