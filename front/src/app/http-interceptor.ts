import { HttpRequest, HttpEvent, HttpHandlerFn, HttpHeaders} from '@angular/common/http'
import { Observable } from 'rxjs';

export function interceptHttpRequests(req: HttpRequest<any>, next: HttpHandlerFn): Observable<HttpEvent<any>> {

  const csrfToken = getCookie('csrftoken');
  const sessionId = getCookie('sessionId');
  if (csrfToken && sessionId) {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken, // Include CSRF token in the request
      'X-SESSION_ID': sessionId, // Include CSRF token in the request
    });
    const cloned = req.clone({
      withCredentials: true,
      headers: headers
    });
    return next(cloned);
  } else {
    return next(req);
  }
}


function getCookie(name: string): string | null {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) {
    return parts.pop()?.split(';').shift() || null;
  }
  return null;
}
