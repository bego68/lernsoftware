import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

// --- Interfaces matching the backend schemas ---

export interface CardContent {
  text: string;
  code?: string;
  image_url?: string;
}

export interface Card {
  id: string; // UUIDs are strings
  deck_id: string;
  front: CardContent;
  back: CardContent;
}

export interface CardReview {
  card_id: string;
  is_correct: boolean;
}

// --- Boss Fight Interfaces ---

export interface BossFightCard extends Card {} // Re-use the Card interface

export interface BossFightSession {
  boss_hp: number;
  cards: BossFightCard[];
}

export interface BossFightAnswer {
  card_id: string;
  answer_is_correct: boolean;
}

export interface BossFightResult {
  correct: boolean;
  damage_dealt: number;
  boss_hp_remaining: number;
  debuff_seconds: number;
}


const API_URL = '/api'; // Using a proxy, will configure this later

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { }

  // --- API Methods ---

  getDueCards(): Observable<Card[]> {
    return this.http.get<Card[]>(`${API_URL}/cards/due`);
  }

  reviewCard(review: CardReview): Observable<any> {
    return this.http.post(`${API_URL}/cards/review`, review, { responseType: 'text' });
  }

  // --- Boss Fight Methods ---

  startBossFight(): Observable<BossFightSession> {
    return this.http.post<BossFightSession>(`${API_URL}/boss-fight/start`, {});
  }

  answerBossFightCard(answer: BossFightAnswer): Observable<BossFightResult> {
    return this.http.post<BossFightResult>(`${API_URL}/boss-fight/answer`, answer);
  }

  // --- User Methods ---

  getUserStats(): Observable<UserStats> {
    return this.http.get<UserStats>(`${API_URL}/user/stats`);
  }
}

export interface UserStats {
  total_xp: number;
  current_level: number;
  badges: string[];
}
