import { ComponentFixture, TestBed } from '@angular/core/testing';

<<<<<<< HEAD
=======
<<<<<<<< HEAD:front/src/app/components/game-summary-list/game-summary-list.component.spec.ts
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
========
>>>>>>> MVE4
import { CopyButtonComponent } from './copy-button.component';

describe('CopyButtonComponent', () => {
  let component: CopyButtonComponent;
  let fixture: ComponentFixture<CopyButtonComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CopyButtonComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CopyButtonComponent);
<<<<<<< HEAD
=======
>>>>>>>> MVE4:front/src/app/components/copy-button/copy-button.component.spec.ts
>>>>>>> MVE4
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
<<<<<<< HEAD
=======

>>>>>>> MVE4
