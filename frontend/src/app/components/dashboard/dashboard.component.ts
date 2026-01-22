import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ApiService, UserStats } from '../../core/api.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './dashboard.component.html'
})
export class DashboardComponent implements OnInit {

  userStats$: Observable<UserStats> | null = null;

  constructor(private apiService: ApiService) { }

  ngOnInit(): void {
    this.userStats$ = this.apiService.getUserStats();
  }
}
