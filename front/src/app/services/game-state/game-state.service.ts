import { Injectable } from '@angular/core';
import {BehaviorSubject} from "rxjs";
import {TournamentMap} from "../../interfaces/tournament-map.interface";

@Injectable({
  providedIn: 'root'
})
export class GameStateService {
  private _dataLoaded = new BehaviorSubject<boolean>(false);
  private _isWaiting = new BehaviorSubject<boolean>(true);
  private _isRemote = new BehaviorSubject<boolean>(true);
  private _lobbyID = new BehaviorSubject<string>('');
  private _isTournament = new BehaviorSubject<boolean>(false);
  private _tournamentMap = new BehaviorSubject<TournamentMap>({rounds_map: {}, winner: null});
  private _activePlayers = new BehaviorSubject<string[]>([]);
  private _lobbyPlayers = new BehaviorSubject<string[]>([]);
  private _lobbyCapacity = new BehaviorSubject<number>(2);
  private _maxPlayers = new BehaviorSubject<number>(2);
  private _canGiveUp = new BehaviorSubject<boolean>(true);

  get dataLoaded$() { return this._dataLoaded.asObservable(); }
  get isWaiting$() { return this._isWaiting.asObservable(); }
  get isRemote$() { return this._isRemote.asObservable(); }
  get lobbyID$() { return this._lobbyID.asObservable(); }
  get isTournament$() { return this._isTournament.asObservable(); }
  get tournamentMap$() { return this._tournamentMap.asObservable(); }
  get activePlayers$() { return this._activePlayers.asObservable(); }
  get lobbyPlayers$() { return this._lobbyPlayers.asObservable(); }
  get lobbyCapacity$() { return this._lobbyCapacity.asObservable(); }
  get maxPlayers$() { return this._maxPlayers.asObservable(); }
  get canGiveUp$() { return this._canGiveUp.asObservable(); }

  setDataLoaded(value: boolean) { this._dataLoaded.next(value); }
  setIsWaiting(value: boolean) { this._isWaiting.next(value); }
  setIsRemote(value: boolean) { this._isRemote.next(value); }
  setLobbyID(value: string) { this._lobbyID.next(value); }
  setIsTournament(value: boolean) { this._isTournament.next(value); }
  setTournamentMap(value: TournamentMap) { this._tournamentMap.next(value); }
  setActivePlayers(value: string[]) { this._activePlayers.next(value); }
  setLobbyPlayers(value: string[]) { this._lobbyPlayers.next(value); }
  setLobbyCapacity(value: number) { this._lobbyCapacity.next(value); }
  setMaxPlayers(value: number) { this._maxPlayers.next(value); }
  setCanGiveUp(value: boolean) { this._canGiveUp.next(value); }

  restrictReset() {
    this.setDataLoaded(false);
    this.setIsWaiting(true);
    this.setCanGiveUp(false);
  }

  reset() {
    this.restrictReset();
    this.setIsRemote(true);
    this.setLobbyID('');
    this.setIsTournament(false);
    this.setTournamentMap({rounds_map: {}, winner: null});
    this.setActivePlayers([]);
    this.setLobbyPlayers([]);
    this.setLobbyCapacity(2);
    this.setMaxPlayers(2);
  }
}
