import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService, BossFightSession, BossFightCard, BossFightResult } from '../../core/api.service';
import { Subscription, interval } from 'rxjs';
import { RouterModule } from '@angular/router';

type GameState = 'loading' | 'intro' | 'fighting' | 'won' | 'lost';

@Component({
  selector: 'app-boss-fight',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './boss-fight.component.html',
  styleUrls: ['./boss-fight.component.scss']
})
export class BossFightComponent implements OnInit, OnDestroy {

  gameState: GameState = 'loading';
  session: BossFightSession | null = null;
  currentCard: BossFightCard | null = null;
  currentIndex = 0;
  showBack = false;

  maxBossHp = 100;
  currentBossHp = 100;

  timeLeft = 180; // 3 minutes for the fight
  timerSubscription: Subscription | null = null;

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.gameState = 'intro';
  }

  startFight(): void {
    this.gameState = 'loading';
    this.apiService.startBossFight().subscribe({
      next: (sessionData) => {
        this.session = sessionData;
        this.maxBossHp = sessionData.boss_hp;
        this.currentBossHp = sessionData.boss_hp;
        this.currentCard = sessionData.cards[0];
        this.gameState = 'fighting';
        this.startTimer();
      },
      error: (err) => {
        console.error('Failed to start boss fight', err);
        this.gameState = 'intro'; // Reset to intro on error
      }
    });
  }

  startTimer(): void {
    this.timerSubscription = interval(1000).subscribe(() => {
      this.timeLeft--;
      if (this.timeLeft <= 0) {
        this.gameState = 'lost';
        if (this.timerSubscription) this.timerSubscription.unsubscribe();
      }
    });
  }

  submitAnswer(isCorrect: boolean): void {
    if (!this.currentCard) return;

    this.apiService.answerBossFightCard({
      card_id: this.currentCard.id,
      answer_is_correct: isCorrect
    }).subscribe({
      next: (result) => {
        this.currentBossHp = result.boss_hp_remaining;
        this.timeLeft -= result.debuff_seconds; // Apply debuff

        if (result.boss_hp_remaining <= 0) {
          this.gameState = 'won';
          if (this.timerSubscription) this.timerSubscription.unsubscribe();
        } else {
          this.goToNextCard();
        }
      },
      error: (err) => console.error('Error submitting answer', err)
    });
  }

  goToNextCard(): void {
    this.currentIndex++;
    if (this.session && this.currentIndex < this.session.cards.length) {
      this.currentCard = this.session.cards[this.currentIndex];
      this.showBack = false;
    } else {
      // All cards answered, but boss not dead -> player loses
      this.gameState = 'lost';
      if (this.timerSubscription) this.timerSubscription.unsubscribe();
    }
  }

  get bossHpPercentage(): number {
    return (this.currentBossHp / this.maxBossHp) * 100;
  }

  ngOnDestroy(): void {
    if (this.timerSubscription) {
      this.timerSubscription.unsubscribe();
    }
  }
}
