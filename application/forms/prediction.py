from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange
from wtforms.fields import SelectField
import datetime 

to_keep = ['Neighborhood', 'Overall_Cond', 'Overall_Qual', 'Kitchen_Qual', 'Exter_Qual', 'Garage_Cars',
            'Misc_Val', 'MS_SubClass', 'surface_total', 'condition_interieur', 'main_score',
            'SalePrice']

class PredictionForm(FlaskForm):
    """Form for prediction
    """
    
    Neighborhood = SelectField(label='Quartier', validators=[
        DataRequired()], choices=['NAmes', 'Gilbert', 'StoneBr', 'NWAmes', 'Somerst', 'BrDale',
                                'NPkVill', 'NridgHt', 'Blmngtn', 'NoRidge', 'SawyerW', 'Sawyer', 'Greens', 'BrkSide', 
                                'OldTown', 'IDOTRR', 'ClearCr', 'SWISU', 'Edwards', 'CollgCr', 'Crawfor', 'Blueste', 
                                'Mitchel', 'Timber', 'MeadowV', 'Veenker', 'GrnHill', 'Landmrk'] , default="NAmes")
    
    Overall_Cond = IntegerField(label='Condition générale (entre 1 et 9)', validators=[
        DataRequired() , NumberRange(min=1, max=9, message="Value must be between 1 and 9")], default=5)
    
    Overall_Qual = IntegerField(label='Qualité générale (entre 1 et 10)', validators=[
        DataRequired() , NumberRange(min=1, max=10, message="Value must be between 1 and 10")], default=5)
    
    Kitchen_Qual = SelectField(label='Qualité de la cuisine', validators=[
        DataRequired()], choices=['Ex', 'Gd', 'TA', 'Fa', 'Po'], default="TA")
    
    Exter_Qual = SelectField(label='Qualité extérieur', validators=[
        DataRequired()], choices=['Ex', 'Gd', 'TA', 'Fa'], default="TA")
    
    Garage_Cars = IntegerField(label="Nombre de voiture entrant dans le garage", validators=[
        DataRequired() , NumberRange(min=0, message="Negative value is not possible")], default=0)
    
    # Surface rénové du garage 
    BsmtFin_SF_first = IntegerField(label="Surface du garage rénové (hors béton) en m2", validators=[
        DataRequired() , NumberRange(min=0, message="Negative value is not possible")], default=0)
    
    # Misc_Val 
    Misc_Val = IntegerField(label="Plus value dans la maison en euros", validators=[
        DataRequired() , NumberRange(min=0, message="Negative value is not possible")], default=0)
    
    MS_SubClass = SelectField(label="Plus value dans la maison", validators=[
        DataRequired()] ,choices=["1-STORY 1946 & NEWER ALL STYLES",
                                 "1-STORY 1945 & OLDER",
                                 "1-STORY W/FINISHED ATTIC ALL AGES",
                                 "1-1/2 STORY - UNFINISHED ALL AGES",
                                 "1-1/2 STORY FINISHED ALL AGES",
                                 "2-STORY 1946 & NEWER",
                                 "2-STORY 1945 & OLDER",
                                 "2-1/2 STORY ALL AGES",
                                 "SPLIT OR MULTI-LEVEL",
                                 "SPLIT FOYER",
                                 "DUPLEX - ALL STYLES AND AGES",
                                 "1-STORY PUD (Planned Unit Development) - 1946 & NEWER",
                                 "1-1/2 STORY PUD - ALL AGES",
                                 "2-STORY PUD - 1946 & NEWER",
                                 "PUD - MULTILEVEL - INCL SPLIT LEV/FOYER",
                                 "2 FAMILY CONVERSION - ALL STYLES AND AGES"], default="1-STORY 1946 & NEWER ALL STYLES")
    
    surface_total = IntegerField(label='Surface totale habitable en m2', validators=[
        DataRequired(), NumberRange(min=0, message="Negative value is not possible")], default=150)
    
    submit = SubmitField(label='prediction')