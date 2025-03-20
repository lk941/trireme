import { NgModule } from '@angular/core';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatButtonModule } from '@angular/material/button';
import { MatMenuModule } from '@angular/material/menu';
import { MatIconModule } from '@angular/material/icon';

@NgModule({
    imports: [
      MatSnackBarModule,
      MatButtonModule,
      MatMenuModule,
      MatIconModule,
    ],
    exports: [
      MatSnackBarModule,
      MatButtonModule,
      MatMenuModule,
      MatIconModule,
    ],
  })
  export class AppModule {}