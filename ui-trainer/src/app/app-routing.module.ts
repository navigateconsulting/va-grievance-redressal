import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { HomeComponent } from './home/home.component';
import { ManageTrainerComponent } from '../app/manage-trainer/manage-trainer.component';
import { TryNowComponent } from '../app/try-now/try-now.component';
import { DeployComponent } from '../app/deploy/deploy.component';
import { ManageActionsComponent } from '../app/manage-actions/manage-actions.component';
import { ManageGrievanceComponent } from '../app/manage-grievance/manage-grievance.component';
import { GrievanceChatComponent } from '../app/grievance-chat/grievance-chat.component';
import { GrievanceAppComponent } from '../app/grievance-app/grievance-app.component';

const routes: Routes = [
      { path: '', redirectTo: 'home/grievance-app', pathMatch: 'full' },
      { path: 'home', component: HomeComponent, children: [
        { path: 'trainer', component: ManageTrainerComponent, children: [
          { path: 'try-now', component: TryNowComponent },
        ] },
        { path: 'deploy', component: DeployComponent },
        { path: 'actions', component: ManageActionsComponent },
        { path: 'grievance-app', component: GrievanceAppComponent },
        { path: 'grievance', component: ManageGrievanceComponent },
        { path: 'grievance-chat', component: GrievanceChatComponent },
      ] },
    ];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
