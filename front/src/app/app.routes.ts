import { Routes } from '@angular/router';
import { SignUpPageComponent } from './pages/sign-up-page/sign-up-page.component';
import { SignInPageComponent } from './pages/sign-in-page/sign-in-page.component';
import { NotFoundPageComponent } from './pages/not-found-page/not-found-page.component';
import { HomePageComponent } from "./pages/home-page/home-page.component";
import { CustomPageComponent } from "./pages/custom-page/custom-page.component";
import { AccountPageComponent } from "./pages/account-page/account-page.component";
import { FriendsPageComponent } from "./pages/friends-page/friends-page.component";
import { AuthGuard } from "./guards/auth.guard";
import { GuestGuard } from "./guards/guest.guard";
import { GamePageComponent } from "./pages/game-page/game-page.component";
import { MonitorPageComponent } from "./pages/monitor-page/monitor-page.component";
import { OnlineGameSelectorPageComponent } from "./pages/online-game-selector-page/online-game-selector-page.component";
import { CreateGamePageComponent } from './pages/create-game-page/create-game-page.component';
import { TournamentPageComponent } from "./pages/tournament-page/tournament-page.component";
import { OauthCallbackComponent } from './components/oauth-callback/oauth-callback.component';

export const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: HomePageComponent, pathMatch: 'full', canActivate: [AuthGuard] },
  { path: 'account', component: AccountPageComponent, pathMatch: 'full', canActivate: [AuthGuard] },
  { path: 'custom', component: CustomPageComponent, pathMatch: 'full', canActivate: [AuthGuard] },
  { path: 'friends', component: FriendsPageComponent, pathMatch: 'full', canActivate: [AuthGuard] },  { path: 'local', component: CreateGamePageComponent, pathMatch: 'full', canActivate: [AuthGuard], data: { gameType: 'local' } },
  { path: 'local', component: CreateGamePageComponent, pathMatch: 'full', canActivate: [AuthGuard], data: { gameType: 'local' } },
  { path: 'local/waiting', component: MonitorPageComponent, pathMatch: 'full', canActivate: [AuthGuard], data: { gameType: 'local' } },
  { path: 'local/:lobby_id/:arena_id', component: GamePageComponent, pathMatch: 'prefix', canActivate: [AuthGuard], data: { gameType: 'local' } },
  { path: 'online', component: OnlineGameSelectorPageComponent, pathMatch: 'full', canActivate: [AuthGuard], data: { gameType: 'online' } },
  { path: 'online/create/options', component: CreateGamePageComponent, pathMatch: 'full', canActivate: [AuthGuard], data: { gameType: 'online' } },
  { path: 'online/create/waiting', component: MonitorPageComponent, pathMatch: 'full', canActivate: [AuthGuard], data: { gameType: 'online', actionType: 'create'} },
  { path: 'online/tournament', component: MonitorPageComponent, pathMatch: 'full', canActivate: [AuthGuard], data: { gameType: 'online', actionType: 'tournament'} },
  { path: 'online/tournament/:lobby_id', component: TournamentPageComponent, pathMatch: 'full', canActivate: [AuthGuard], data: { gameType: 'online', actionType: 'tournament'} },
  { path: 'online/tournament/:lobby_id/:arena_id', component: TournamentPageComponent, pathMatch: 'full', canActivate: [AuthGuard], data: { gameType: 'online'} },
  { path: 'online/join', component: MonitorPageComponent, pathMatch: 'full', canActivate: [AuthGuard], data: { gameType: 'online' , actionType: 'join'} },
  { path: 'online/join/:lobby_id', component: MonitorPageComponent, pathMatch: 'full', canActivate: [AuthGuard], data: { gameType: 'online', actionType: 'join_specific'} },
  { path: 'online/:lobby_id/:arena_id', component: GamePageComponent, pathMatch: 'prefix', canActivate: [AuthGuard], data: { gameType: 'online' } },
  { path: 'oauth-callback', component: OauthCallbackComponent, pathMatch: 'prefix', canActivate: [GuestGuard] },
  { path: 'sign-in', component: SignInPageComponent, pathMatch: 'full', canActivate: [GuestGuard] },
  { path: 'sign-up', component: SignUpPageComponent, pathMatch: 'full', canActivate: [GuestGuard] },
  { path: '404', component: NotFoundPageComponent, pathMatch: 'full' },
  { path: '**', redirectTo: '/404' },
];
