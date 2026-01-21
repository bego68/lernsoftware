import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, BehaviorSubject, tap } from 'rxjs';

const API_URL = '/api';

export interface AuthToken {
  access_token: string;
  token_type: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private authToken = new BehaviorSubject<string | null>(null);
  private loggedIn = new BehaviorSubject<boolean>(false);

  isLoggedIn$ = this.loggedIn.asObservable();

  constructor(private http: HttpClient, private router: Router) { }

  login(username: string, password: string): Observable<AuthToken> {
    const headers = { 'Content-Type': 'application/x-www-form-urlencoded' };
    const body = new HttpParams()
      .set('username', username)
      .set('password', password);

    return this.http.post<AuthToken>(`${API_URL}/token`, body.toString(), { headers }).pipe(
      tap(response => {
        this.authToken.next(response.access_token);
        this.loggedIn.next(true);
      })
    );
  }

  logout(): void {
    this.authToken.next(null);
    this.loggedIn.next(false);
    this.router.navigate(['/login']);
  }

  getToken(): string | null {
    return this.authToken.getValue();
  }
}
