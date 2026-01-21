import { Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { LearnComponent } from './components/learn/learn.component';
import { BossFightComponent } from './components/boss-fight/boss-fight.component';
import { LayoutComponent } from './components/layout/layout.component';
import { authGuard } from './core/auth.guard';

export const routes: Routes = [
    { path: 'login', component: LoginComponent },
    {
        path: '',
        component: LayoutComponent,
        canActivate: [authGuard],
        children: [
            { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
            { path: 'dashboard', component: DashboardComponent },
            { path: 'learn', component: LearnComponent },
            { path: 'boss-fight', component: BossFightComponent },
        ]
    },
    // Redirect to login if no other route matches
    { path: '**', redirectTo: 'login' }
];
