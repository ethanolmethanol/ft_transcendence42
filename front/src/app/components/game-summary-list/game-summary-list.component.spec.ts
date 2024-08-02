import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GameSummaryListComponent } from './game-summary-list.component';

describe('GameSummaryListComponent', () => {
  let component: GameSummaryListComponent;
  let fixture: ComponentFixture<GameSummaryListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GameSummaryListComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GameSummaryListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

