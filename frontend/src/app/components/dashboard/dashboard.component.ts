import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ApiService, UserStats } from '../../core/api.service';
import { Observable } from 'rxjs';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatDividerModule } from '@angular/material/divider';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    MatCardModule,
    MatButtonModule,
    MatDividerModule,
    MatIconModule
  ],
  templateUrl: './dashboard.component.html'
})
export class DashboardComponent implements OnInit {

  userStats$: Observable<UserStats> | null = null;

  constructor(private apiService: ApiService) { }

  ngOnInit(): void {
    this.userStats$ = this.apiService.getUserStats();
  }
}
