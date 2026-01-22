import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService, Card } from '../../core/api.service';

@Component({
  selector: 'app-learn',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './learn.component.html'
})
export class LearnComponent implements OnInit {

  dueCards: Card[] = [];
  currentCard: Card | null = null;
  currentIndex = 0;
  showBack = false;
  isLoading = true;
  sessionFinished = false;

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.loadDueCards();
  }

  loadDueCards(): void {
    this.isLoading = true;
    this.apiService.getDueCards().subscribe({
      next: (cards) => {
        this.dueCards = cards;
        if (this.dueCards.length > 0) {
          this.currentCard = this.dueCards[0];
        } else {
          this.sessionFinished = true;
        }
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Failed to load due cards', err);
        this.isLoading = false;
        // TODO: Show user-friendly error message
      }
    });
  }

  revealCard(): void {
    this.showBack = true;
  }

  submitAnswer(isCorrect: boolean): void {
    if (!this.currentCard) return;

    this.apiService.reviewCard({
      card_id: this.currentCard.id,
      is_correct: isCorrect
    }).subscribe({
      next: () => {
        this.goToNextCard();
      },
      error: (err) => {
        console.error('Failed to submit review', err);
        // TODO: Handle error, maybe retry?
      }
    });
  }

  goToNextCard(): void {
    this.currentIndex++;
    if (this.currentIndex < this.dueCards.length) {
      this.currentCard = this.dueCards[this.currentIndex];
      this.showBack = false;
    } else {
      this.currentCard = null;
      this.sessionFinished = true;
    }
  }
}
