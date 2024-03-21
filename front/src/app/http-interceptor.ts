import { HttpRequest, HttpEvent, HttpHandlerFn, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

export function interceptHttpRequests(req: HttpRequest<any>, next: HttpHandlerFn): Observable<HttpEvent<any>> {
  let headers = new HttpHeaders({
    'Content-Type': 'application/json'
  });
  headers = addHeader(headers, 'X-CSRFToken', 'csrftoken');
  const cloned = req.clone({
    withCredentials: true,
    headers: headers
  });
  return next(cloned);
}

function addHeader(headers: HttpHeaders, headerName: string, cookieName: string): HttpHeaders {
  const value = getCookie(cookieName);
  if (value) {
    headers = headers.set(headerName, value);
  } else {
    console.log(`No value found for ${cookieName}`);
  }
  return headers;
}

function getCookie(name: string): string | null {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) {
    return parts.pop()?.split(';').shift() || null;
  }
  return null;
}
